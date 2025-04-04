USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_TenderInfo]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_TenderInfo](
	[TenderID] [int] IDENTITY(1,1) NOT NULL,
	[AccountNumber] [varchar](200) NOT NULL,
	[RoutingNumber] [varchar](200) NOT NULL,
	[BankName] [varchar](50) NOT NULL,
 CONSTRAINT [PK_vg_TenderInfo] PRIMARY KEY CLUSTERED 
(
	[TenderID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
