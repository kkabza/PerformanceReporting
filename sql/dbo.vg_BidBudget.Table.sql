USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_BidBudget]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_BidBudget](
	[BidBudgetID] [int] IDENTITY(1,1) NOT NULL,
	[UserID] [uniqueidentifier] NOT NULL,
	[ActivityDate] [datetime] NOT NULL,
	[BudgetAmount] [decimal](18, 2) NOT NULL,
	[VGProductID] [int] NOT NULL,
 CONSTRAINT [PK_vg_BidBudget] PRIMARY KEY CLUSTERED 
(
	[BidBudgetID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[vg_BidBudget] ADD  CONSTRAINT [DF_vg_BidBudget_ActivityDate]  DEFAULT (getdate()) FOR [ActivityDate]
GO
