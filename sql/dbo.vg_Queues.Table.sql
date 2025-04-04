USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_Queues]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_Queues](
	[QueueID] [int] IDENTITY(1,1) NOT NULL,
	[ItemCount] [int] NOT NULL,
	[AuctionStartDate] [datetime] NULL,
	[AuctionEndDate] [datetime] NULL,
	[QueueValue] [decimal](18, 2) NOT NULL,
	[Status] [int] NOT NULL,
	[AuctionId] [int] NOT NULL,
 CONSTRAINT [PK_Batch_Tbl] PRIMARY KEY CLUSTERED 
(
	[QueueID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[vg_Queues] ADD  CONSTRAINT [DF_Batch_Tbl_Status]  DEFAULT ((0)) FOR [Status]
GO
